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

## FLOOR at 12:30 (handover written by the 10:27 seat at ~78%, rotating inside 80-90)
- **D 53rd** %161 (Opus): KINTSUGI deploy at PIN 07a2d62be6a0 (058 + PR 2003 + PR 2005 + PR 2004; NOT PR 2006). GO KINTSUGI sent 01:11:52Z naming the 058 window. Building k18 (2 batches) since 01:15:19Z. Then: post-build checks -> ls-remote -> migrate058_d53 CHECK -> APPLY -> b-post + cescope (predicted 0/14/0/14, certifications 1) -> part a (vc-issuer, originate) -> vprobe MID -> part b api-gateway -> +15 min error counter (ANSI-aware, controls proven) -> STATUS B. STOP list: any guard, >1 Applying line, error naming charge_events/metering/RLS, KS-535 equality, OOM. Never alter the policy (a new decision for Kam).
  - On STATUS B: verify REVISION/claims, ACK + wrap, score, pane_close; REPORT TO KAM on the panel: kintsugi carries everything merged before PR 2006; his kintsugi count tenant-less 0 of 14; 058 changed behaviour on kintsugi (unscoped charge_events reads 14 -> 0, certifications opened) per his card 1005 a; Platform S / bot impact UNMEASURED; the swap windows AEDT.
- **B 95th** %162 (Sonnet): PR 2006 MERGED 01:26:04Z as 5fc5569ed96a (verified at origin by Wednesday). WRAPPING on Wednesday's ACK. On its wrap mail: verify history '^## .*Seat B 95' = 1 (control B 94 = 1), HANDOVER FINAL, score (~0.95), pane_close %162.
- develop now = 5fc5569ed96ac61f64823cc9e1fa841899aa1f62 (PR 2006). KS-1990 needs a LATER kintsugi deploy (demo frozen).
- Wrapped + scored this seat: S 19th 0.94, D 52nd 0.97, W 28th 0.95 (gate 195 GO WITH NOTES -> merged). Gate 195 done.

## THEN (owed, in order)
1. D 53rd STATUS B -> verify, ACK, score, close, report to Kam (see floor).
2. B 95th wrap -> score, close. A later kintsugi round for PR 2006 (5fc5569ed96a) + anything merged after.
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
