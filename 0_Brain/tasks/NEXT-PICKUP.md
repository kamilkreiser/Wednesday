---
date: 2026-11-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 11:47 AEDT 2026-11-05 by the 10:27 rotation seat (67% checkpoint). Previous kept as NEXT-PICKUP.md.pre-1105-1147. Replace wholesale; never stack.
---

# NEXT PICKUP — Thu 5 Nov 2026, 11:47 (the 10:27 rotation seat)

## KAM TODAY (live board, view=wednesday; read with kam_rulings_today.sh 11:46:57; newest 09:05:06)
- 07:07:25 card wed-morning-fleet-activity-1105 = a (plan stands). 07:08:03 card secuura-ks1401-058-merge-demo-billing-1104 = a ("Merge; I stop every demo redeploy until you say"). 07:08:39 "but deploy everything now. so both systems have all changes. new demo rule takes affect after this deploy". 09:05:06 card secuura-pr2004-ks1986-gate192-hold-1105 = a (DONE: fixed, gated, merged, KS-1991 filed).
- **DEMO IS NOW FROZEN** (D 52nd deployed 07a2d62be6a0 at 10:39-10:48 AEDT; Kam told on the panel bf-eee33c8d70db). NO demo redeploy without Kam's word. Every Secuura deploy brief carries this.
- Standing: Spark IGNORED until he says (11-04 16:42); October deploy grant extended until further notice; 11-04 09:16 'clear and close as many in progress tickets as possible'.
- Personal errand done 11:12: ~/Downloads/winmail.dat unpacked into ~/Downloads/winmail_extracted (contents not read).

## FLOOR at 11:47
- **D 53rd** %161 (Opus): KINTSUGI deploy of develop 07a2d62be6a0 (058 + PR 2003 + PR 2005 + PR 2004). Brief: 2_Project_Files/fleet/briefs_staged/2026-11-05_seatD53_deploy_kintsugi.md. Stops at STATUS A for 'GO KINTSUGI at <pin12> (Seat D 53rd)'. **Expect QUESTION 'ks1401 058 window'** if 058's tenant_isolation policy is missing on any kintsugi table (D 52nd's warning: the migration would change OLD code's reads before the swap). Plan confirmation = rung 6 owed. Before GO: ls-remote develop, kam_rulings, no other GO outstanding.
- **GATE 195** (Sonnet subagent, TIER 2, round 1 of 2) on PR 2006 (KS-1990, head 6311c141f99e, develop 07a2d62be6a0): commission 0_Brain/reference/2026-11-05_gate195-ks1990-pr2006/commission.md. **A rotation KILLS it: if verdict.md line 1 reads the INCOMPLETE stub or is absent at the successor's boot, RE-COMMISSION from commission.md.** On a GO: a merge seat (Sonnet, C5) on Wednesday's head-pinned GO under the TESTED grant; it then needs a kintsugi deploy later (demo frozen).
- Seats wrapped + scored this seat: S 19th 0.94 (11 tickets KS-1992..2002 + 2 comments), D 52nd 0.97 (demo), W 28th 0.95 gate pending (PR 2006). All panes closed.

## THEN (owed, in order)
1. D 53rd plan confirmation -> STATUS A -> (058 window ruling) -> GO KINTSUGI -> STATUS B -> report Kam his kintsugi tenant-less charge count with the deploy.
2. Gate 195 verdict -> completion check -> merge seat for PR 2006 (or round 2).
3. CLOSE-OUT seat after D 53rd STATUS B: tickets deployed to BOTH boxes (D 52nd's evidence/F6_ticket_table.tsv + D 53rd's table): KS-1823, KS-1401 first; KS-1256/1561/1459/1458/1868 slices; KS-1958/1959/1986. Board writes only, per-ticket evidence.
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
