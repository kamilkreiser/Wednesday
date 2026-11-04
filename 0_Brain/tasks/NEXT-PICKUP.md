---
date: 2026-11-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 03:1x AEDT 2026-11-05 by the 22:0x (11-04) seat. The stacked 11-04 file is kept as NEXT-PICKUP.md.pre-1105-0315. Replace wholesale; never stack.
---

# NEXT PICKUP — Thu 5 Nov 2026, 03:1x (the 22:0x seat's handover)

## KAM'S INSTRUCTION IN FORCE
2026-11-04 09:16 (new account): "new account logged in.  Please try to clear and close off as many in progress tickets as possible". Grant row in EXPIRING-GRANTS. October deploy grant (both boxes, kintsugi first) extended "until further notice". Spark IGNORED until he says (16:42 11-04: backing up G drive to Synology).

## STATE (all verified at source by Wednesday unless marked)
- develop = 035685291b9d (PR 2000 squash). Merged since the GitHub lift: 1798 (536642104002), 2001 (6a36d41b9852, KS-1256 + migration 057), 2000 (035685291b9d, KS-1561 r2).
- KINTSUGI = 035685291b9d (D 51st STATUS B 14:59Z, all checks = predicted, rollback tag pre-20261104k17; RELAYED: Wednesday cannot reach the box). Migration 057 applied there (tracker 58). DEMO untouched (REVISION e3d8456ec81d per D 50th; needs 056+057).
- Kintsugi Redis holds NO platform-settings key (13:43Z and 14:57Z, TTL -2): no connector allow-list in force there. KS-1256's fix makes settings durable once an admin re-saves.
- FLOOR: EMPTY (no seat live). GitHub incident (09:49-11:30Z) mitigated; git working since 11:33Z.
- Closes verified tonight: KS-1603, 1679, 1683, 1836 (W 27th), KS-1244 (D 51st), KS-1340 (S 18th). Filed tonight: KS-1983..KS-1990 (S 18th, verified).

## WAITING ON KAM (cards / rulings)
- **secuura-ks1401-058-merge-demo-billing-1104** (posted 23:39 11-04; rec a; default = PR 2002 stays UNMERGED). Gate 190 GO WITH NOTES — HOLD-FOR-KAM: F1 any later demo redeploy auto-applies 058; F2 tenant-less charge rows join the default tenant's metering totals. On a: QUEUE PR 2002 to a merge seat (gate tree 1c8e329f1233 was on 536642104002: RECOMPUTE onto develop), write a hard STOP into every Secuura deploy brief (no demo redeploy from a develop containing 058 without his word), kintsugi deploy reports the tenant-less charge_events count to Kam BEFORE applying 058. On b: merge, no demo stop. On c: hold. Then `decision_queue.sh --delivered`.
- New tickets needing his ruling (put on the MORNING CARD, counts only per rule 10a, or a card each if he asks): KS-1983 (seeded demo-account passwords on the breach list: exempt by design, or rotate/gate), KS-1958 (G152-F1: availability vs fail-closed on a revoked credential), KS-1986 (v1 vs v2 verify judge the original over different tenant scopes).

## MORNING CARD (10a) — the 06:00 seat writes it; content owed from this seat
1. Night summary: 3 merges, kintsugi deploy (no rollback), 6 closes verified, 8 filed, GitHub outage 09:49-11:30Z handled (the 21:1x 'check your SSH keys' card was WITHDRAWN at 22:03: GitHub's incident, not our keys).
2. Wednesday's rulings he should know: (a) KS-1244 — whether Platform S / the WhatsApp bot send x-api-key twice was UNMEASURABLE; ruled swap with a 30-min watch + instant rollback (REAL 0 in a quiet window); (b) the kintsugi Redis reads used the gateway container's own REDIS_URL inside the container (inside his KS-1233 card b); (c) gate 188 r2's HOLD on KS-1561 ruled not standing (FYI bf-4a6d42145f18, hold offered, none received); (d) KS-1256 item-6/F4 inside the accepted row.
3. Kintsugi has no allow-list in force (Redis key absent) — an admin settings save restores it.
4. Awaiting him: Secuura/Blockchain 1 card (PR 2002) + 3 ticket rulings (KS-1983, KS-1958, KS-1986).
5. Plan: DEMO round (D 52nd) when he is up — demo was never touched tonight; it needs 056+057; NEVER 058 without his word.

## OWED (Wednesday's)
- DEMO deploy round (D 52nd): brief from D 51st's HANDOVER (5_Project_History/2026-11-05_seatD-51st/HANDOVER.md, FOR A SUCCESSOR: demo starting facts, KS-535 priors, 057 for demo's tracker); demo is UAT (Peter tests there): run it in Kam's day, kintsugi-first already satisfied; same KS-1244 watch on demo.
- Post-deploy closes still open (comments posted by D 51st): KS-1256, KS-1561, KS-1459, KS-1458, KS-1868 slices, KS-1234 (NODE_ENV=development on kintsugi: production-mode 307 cannot be shown there), KS-1233 (TTL -1 confirmable only after a settings read refills the key). A read-only probe design or Kam's acceptance closes them.
- KS-1990 (seed-demo-users 200 with 14 failed) needs a fresh disposable stack run to find the cause (a W-lane stack seat).
- E 35th's five filing candidates (0_Brain/reference/2026-11-04_gate189-ks1256-pr2001/ready_2001.txt) were NOT in S 18th's list: route to the next filing seat.
- Secuura launcher (Secuura's file) runs `git ls-remote` at boot before a seat can read a fleet git pause; also names coagent@ (404) and says CC Kam. Route via a Secuura seat's brief if pauses recur.
- PR 1383 (KS-1401 draft): close as superseded only AFTER PR 2002 merges.
- KS-911/912 launcher by-hash change: live sha matches neither gated nor shipped — investigate or card.
- CONTRIBUTING N/13 vs TOTAL_LEGS=16 belongs in Stuart's KS-1366 (draft at Secuura 5_Project_History/2026-11-04_seatU-12th/drafts/T5_contributing_legs.md); route (Kam's call how).
- Carried: @azure/msal-node baseline dies MON 2026-11-09 (check its ticket); WED-155 (inbox_digest key in argv); boot-prompt MODEL CHOICE line; INDEX.md refresh (last 10-27); stash@{0} never drop.

## RULES LEARNED TONIGHT (this seat; ledger rows written)
- When an external service fails for EVERY credential at once, read the vendor's status API (githubstatus.com/api/v2/incidents/unresolved.json) before any theory reaches a seat or a card.
- Where a secret or config value lives on a box Wednesday cannot read: write 'UNMEASURED: locate it read-only, propose the route, wait for a ruling' — never a route; every such route carries an 'empty source = stop' guard.
- A close list in a brief is built from each ticket's TITLE + scope, never from another seat's deploy-surface column; a card cited for 'what to file' is quoted from its option text.
- A refusable step (pane_close, send, card) is its own call; the note copies its success line verbatim.
- Gate commissions: specific part + `2_Project_Files/fleet/qa-agent/gate_common.md` concatenated into `<workdir>/commission.md`; round 2 writes `verdict_r2.md`.
