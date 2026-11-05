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

## FLOOR (14:19, refreshed at the 65% checkpoint)
- **D 54th %166 (Opus): KINTSUGI deploy of develop 5fc5569ed96a (PR 2006, KS-1990).** It stops at STATUS A. Owed next: read its PLAN CONFIRMATION + STATUS A WHOLE; GO by mail with the subject 'GO KINTSUGI at 5fc5569ed96a (Seat D 54th)' (add 'incl anchoring m365-integration tenant-provisioning' ONLY if its contentfp shows real older code AND you decide the window is worth it; default = no). Demo is frozen; nothing goes there.
- Closed and scored this seat: S 20th 0.94 (KS-1401, KS-1823 Done), U 13th 0.96 (KS-1584, 1612, 1860, 1230 Done), S 21st 0.94 (KS-2003/2004/2005 filed, comment on KS-1959). All verified on Linear by Wednesday.
- Census of the KS In Progress set: 0_Brain/reference/2026-11-05_ks-inprogress-postdeploy/ (205 tickets; most of the rest are SCOPE-REMAINS / HUMAN-OWNED / KAM-DECISION).

## DONE THIS SEAT (also)
- Mechanism (a) BUILT: note_entry.sh RECEIPT-VERB GUARD. Any note saying answered / closed %N / acked %N / ruled: / delivered needs --receipt <file written in the last 120 s>: `cmd > f 2>&1`, read it, then `note_entry.sh --receipt f --stdin`. Override NOTE_ALLOW_RECEIPT_VERB=1 with the reason. Arms tests/note_entry_receiptverb_arms.sh 12/12. Quote sends in DOUBLE quotes inside a note (the sent-log guard's regex ends a quote at " only).
- NAS answer (bf-0f2f069fdbdd693f); Kam 13:21 'The device comes tomorrow.  We can evaluate then' (item 6 below).

## THEN (owed, in order)
1. D 54th: plan, STATUS A, GO, STATUS B, wrap, score, close (see FLOOR).
2. **KS-911/912** (KS-907 launcher + suite residues): launch ONLY when no Secuura seat is live (it edits the project launcher). Next window = after D 54th wraps (it is launched from the project launcher).
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
