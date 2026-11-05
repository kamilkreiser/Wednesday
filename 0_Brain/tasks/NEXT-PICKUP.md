---
date: 2026-11-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 11:47 AEDT 2026-11-05 by the 10:27 rotation seat (67% checkpoint). Previous kept as NEXT-PICKUP.md.pre-1105-1147. Replace wholesale; never stack.
---

# NEXT PICKUP — Thu 5 Nov 2026, 11:54 (the 10:27 rotation seat; floor refreshed at 70%)

## KAM TODAY (live board, view=wednesday; read with kam_rulings_today.sh 11:46:57; newest 09:05:06)
- 07:07:25 card wed-morning-fleet-activity-1105 = a (plan stands). 07:08:03 card secuura-ks1401-058-merge-demo-billing-1104 = a ("Merge; I stop every demo redeploy until you say"). 07:08:39 "but deploy everything now. so both systems have all changes. new demo rule takes affect after this deploy". 09:05:06 card secuura-pr2004-ks1986-gate192-hold-1105 = a (DONE: fixed, gated, merged, KS-1991 filed).
- **DEMO IS NOW FROZEN** (D 52nd deployed 07a2d62be6a0 at 10:39-10:48 AEDT; Kam told on the panel bf-eee33c8d70db). NO demo redeploy without Kam's word. Every Secuura deploy brief carries this.
- Standing: Spark IGNORED until he says (11-04 16:42); October deploy grant extended until further notice; 11-04 09:16 'clear and close as many in progress tickets as possible'.
- Personal errand done 11:12: ~/Downloads/winmail.dat unpacked into ~/Downloads/winmail_extracted (contents not read).

## FLOOR at 12:58 (handover from the 10:27 seat, rotating)
- **D 53rd** %161: KINTSUGI DEPLOYED 07a2d62be6a0 (STATUS B 01:57Z), verified; 058 applied in a 7 s window; Kam TOLD on the panel 12:5x (bf-462d6704bc5e). WRAPPING on Wednesday's ACK. On its wrap mail: verify history '^## .*Seat D 53' = 1 (control D 52 = 1), HANDOVER FINAL, score (~0.97), pane_close %161 (alone, then the note in the NEXT message).
- BOTH BOXES now run 07a2d62be6a0. develop = 5fc5569ed96ac61f64823cc9e1fa841899aa1f62 (PR 2006, KS-1990) is NOT on either box. DEMO IS FROZEN (Kam 07:08); kintsugi gets PR 2006 in a later round under the October grant.
- No other seat live. Capacity ROOM.

## FIRST TASK OF THE NEXT SEAT (ledger w=4 regression, 2026-11-05)
- Build mechanism (a): tools/note_entry.sh refuses a body carrying a receipt verb (answered, closed %, acked, ruled:, delivered) unless --receipt <file> names a tool output written in the last 120 s. note_entry is SHARED with Tuesday: mail her a coordination FYI (done for the ACK-HASH GUARD at 12:0x). Arms both ways, copy+mv install, backup .pre-*.

## THEN (owed, in order)
1. D 53rd wrap -> verify, score, close.
2. B 95th wrap -> score, close. A later kintsugi round for PR 2006 (5fc5569ed96a) + anything merged after.
3. CLOSE-OUT seat NOW (both boxes at 07a2d62be6a0): KS-1401 CLOSE-READY (D 53rd + D 52nd evidence), KS-1823 CLOSE-READY (D 52nd); tickets deployed to BOTH boxes (D 52nd's evidence/F6_ticket_table.tsv + D 53rd's table): KS-1823, KS-1401 first; KS-1256/1561/1459/1458/1868 slices; KS-1958/1959/1986. Board writes only, per-ticket evidence.
4. **KS-911/912** (KS-907 launcher + suite residues): launch ONLY with no Secuura seat live (the fix edits the project launcher; live seats' launcher bash still runs from it — never edit a running script).
5. Filing seat (small): G191-F3 by-hash 500 + store/selectList err?.message (named in KS-1959 text); Schemathesis leg B (demo_seed_gate.py) red after PR 2006; org-link empty catch adminConfig.ts:2145; KS-1990 W 28th candidates.
6. KS-960 (users.email schema authority, 'DO NOT RECONCILE'): now carries the KS-1990 42P10 proof — a card for Kam when the merged evidence shows it blocks first-run seeding (KS-915 relies on it).
7. Carried: WED-155 (inbox_digest key in argv); INDEX.md refresh (last 10-27); stash@{0} never drop. msal 11-09 fuse RETIRED (b4d5f56d1; EXPIRING-GRANTS updated).

## OPEN FAULT
- Mail Wednesday -> secuura-blockchain@: two ACKs to D 52nd (00:20:46Z, 00:25:02Z) never arrived; self-probe arrived in 7 s and a direct probe to secuura-blockchain@ in ~15 s (00:43Z); the D 53rd brief verified at destination 00:44:40Z. Cause UNMEASURED. send_brief --kind answer does NOT verify at destination: after every answer, the cockpit say --mail tap IS the delivery check (rc 5 = not delivered -> re-send/probe).

## RULES APPLIED THIS SEAT
- New mechanism: note_entry.sh ACK-HASH GUARD (a note quoting a wake_ack hash must match the stored one). After wake_ack, the note goes in the NEXT message.
- A brief's provenance block is three-field (fact | source | read date) with owner-qualified paths, or send_brief refuses.
- D 52nd's 058 warning carried into D 53rd's brief as a QUESTION gate before GO.
