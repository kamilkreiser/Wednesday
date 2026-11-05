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

## FLOOR (13:1x)
- No seat live. D 53rd CLOSED (13:03, score ~0.97). B 95th CLOSED (12:33, 0.95).
- S 20th close-out brief: Sonnet drafter commissioned 13:1x -> briefs_staged/2026-11-05_seatS20_closeout.md. Wednesday reads it WHOLE, re-checks OTHER_SEATS, dry run, launch with SEAT_MODEL_ENV=claude-sonnet-5-5.

## DONE THIS SEAT
- Mechanism (a) BUILT: note_entry.sh RECEIPT-VERB GUARD (answered / closed %N / acked %N / ruled: / delivered need a --receipt file written in the last 120 s; override NOTE_ALLOW_RECEIPT_VERB=1). Arms tests/note_entry_receiptverb_arms.sh 12/12. Tuesday FYI sent. **Every note that reports a step's outcome now needs the step's output in a file: `cmd > f 2>&1`, read it, then note_entry.sh --receipt f --stdin.**

## THEN (owed, in order)
1. S 20th close-out: launch, rung 5/6, its STATUS -> verify per ticket on the board, score, close.
2. **KS-911/912** (KS-907 launcher + suite residues): launch ONLY when no Secuura seat is live (it edits the project launcher). Next window = after S 20th wraps.
3. Filing seat (small): G191-F3 by-hash 500 + store/selectList err?.message (KS-1959 text); Schemathesis leg B (demo_seed_gate.py) red after PR 2006; org-link empty catch adminConfig.ts:2145; KS-1990 W 28th candidates.
4. A kintsugi round for PR 2006 (5fc5569ed96a) + anything merged after, under the October grant (kintsugi only; demo frozen).
5. KS-960 (users.email schema authority, 'DO NOT RECONCILE'): card for Kam when the merged evidence shows it blocks first-run seeding.
6. **NAS evaluation FRIDAY 2026-11-06** (Kam 13:21:06 live: "The device comes tomorrow.  We can evaluate then"; receipt bf-1efdfc9d3103f370). Owed then: measure the fitted RAM + slots on the device, read UGREEN's UGOS Pro Docker docs (rate-limited 11-05), and propose the supervised pilot (one Secuura disposable test stack via an SSH docker context) as a CARD with a default of HOLD. Nothing moves before his word.
7. **w=3 REGRESSION, mechanism owed (ledger 2026-11-05 13:3x):** a PreToolUse ADVISORY (claim first; hooks are shared) on `grep -r` / `find` over 0_Brain/reference, any 5_Project_History, local-model/spark/runs or night/ trees: 'scope it with --include + a named dir, or stop it by pid if the harness backgrounds it'. Arms: a bare recursive grep there fires; a scoped one does not.
8. From S 20th's STATUS: KS-1384 (Stuart's ticket) shows 'fix strings live 16 of 17' on demo (D 52nd table): one fix string is not live there and nobody has chased it. Measure which string (read-only, a seat), then card or file. KS-1841 owns the api-gateway docs allowlist.
9. **Record-defect sweep owed (U 13th finding 4, 03:03Z):** the U 11th/U 12th box-read templates (boxread_c/_d) query admin_settings for allowedDocumentTypes, but PUT /api/admin/settings never wrote there (Redis, then svc_gateway_settings since KS-1256). Any 11-04 close or comment that said 'no allow-list stored' rests on the wrong table. A seat reads U 11th/U 12th HANDOVERs + closeout tables, lists every ticket whose evidence used those templates, and re-reads the right store (read-only) or posts a corrective comment. Also from U 13th: secuura-demo-service Exited (1) on BOTH boxes (9 days); kintsugi anchoring/m365/tenant-provisioning still on 11-04 images (next deploy round).
10. Carried: WED-155 (inbox_digest key in argv); INDEX.md refresh (last 10-27); stash@{0} never drop.

## OPEN FAULT
- Two Wednesday ACK mails to D 52nd never arrived (cause UNMEASURED). send_brief --kind answer does NOT verify at destination: after every answer, the cockpit say --mail tap IS the delivery check.
