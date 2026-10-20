---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 12:5x Wednesday seat (Sonnet 5.5) at its ~50% checkpoint (13:3x AEDT, ctx 46%); UPDATED 13:5x at the 50% checkpoint. Replace wholesale again; never stack. Previous versions: git history + NEXT-PICKUP.md.pre-1020-1338.
---

# NEXT PICKUP (Tue 20 Oct, written 13:3x AEDT by the 12:5x seat)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says (the by-tier digest is ~600 KB: read lines 1-2200 whole, then the headlines list `grep -n '^## '` from 2200, then the routing/merge/rotation rules near the end; the tool caps reads per turn). Then `tools/kam_rulings_today.sh`, `reconcile_rulings.py`, `tools/newmail.sh` (seen-ids persist in /private/tmp/wed_newmail), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` with the LITERAL path (a `$C` variable trips the no-cd hook). Gate verdict: `sed '1d;$d' verdict.md | shasum -a 256` equals its trailer; move any stray file a gate leaves (verdict.md.tmp) to the scratchpad quarantine.
3. send_brief / brief_and_launch need `WED_AGENT=wednesday`. Subjects never carry hold/stop/checkpoint. Send, tap (`cockpit.sh say "<cockpit NAME>" "<pointer>" --mail "<subject substring>"`) and note are THREE separate calls; a note must not say posted/sent in the same command as the send (receipt guard). brief_and_launch demands: provenance `fact | source | read YYYY-MM-DD`, a ticket-state line for every ticket in the QUEUE, a `RULED BY KAM, NOT YET IN AN ARTEFACT` heading, and a SELF-CHECK line copied from the gate's own print.
4. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant "until further notice", TESTED merge grant, merge-and-archive grant. Kam 13:0x terminal: "spark connected. please use it as well".

## 1. LIVE FLOOR (14:1x, ctx 65%) - develop = f01ba49da56d3d55204caa02ab3348f94d63b9c0; Secuura merges today 19; usage gauge 80% (the 80-90 band binds: cloud launches only if it matters and nothing local can do it; hard stop 90%, ~3 h at today's rate; Kam told bf-f4e5ba945632)
Merged and verified by fetch: #1645 #1646 #1648 #1647 #1649 #1650 #1651 #1652 #1653 #1658 #1656 #1655 #1657 #1660 #1659 #1661 #1662 #1665 #1663(r2). Kintsugi at 89956fe92956; demo d75bfe2deb80.
SEATS (pane ids from `tmux list-panes -t fleet:0`): R 59th %21 (Sonnet, ~70%+), G 13th %22, C 32nd %23, D 26th %24, E %25 (all Opus 5 as launched; model switches skipped).
- **R 59th:** #1664 (KS-1687) gate CG1 round 2 = GO WITH NOTE at efd79bc87b36; RULED: R pushes ONE comment-only commit (N3 test comments/K5 title, relocate the JSDoc, N2 wording; no code, no cell), I check the delta is comments + one test title and GO the NEW head with no further gate. #1668 (BZ1 N1-N3 follow-up, head b275a072e0fe, landing 355fafd1bf8c) at gate CH1 (Sonnet, running). Then KS-1689 (Kam d): needsReauth = connected && no refreshToken, one status read, tier 2, no OpenAPI.
- **G 13th:** #1669 (KS-1692 PR 1, head 4728c1d61303, landing 9c7962e77f2a) at gate CI1 (Opus, running). #1666 (KS-758 b) gate CE1 GO WITH NOTE but SUPERSEDED by Kam's (c): round 2 = ref_hmac via lookupHash (plan confirmed: warn when the key is unregistered, correlator in the body, three CE1 test gaps closed). KS-1692 PR 2 ruled shape (i) discriminated return, build after PR 1's GO. KS-1696 filed (deletion-log cross-tenant read).
- **C 32nd:** #1667 (KS-1695 gap 1, head d7c2e296c909) gate CF1 GO WITH NOTE; RULED round 2 (isPlatformRole only, platform_admin stays 404 + a cell + a ticket; two test-gap cells; residue); KS-1699 filed (verify/share/recertify ungated writes), KS-1697 filed. On READY: Opus gate round 2.
- **D 26th:** raising the two held Spark passes (KS-1116 vc-issuer, KS-1679 originate), Sonnet-tier work on Opus 5; PR A committed at 67f83d4d1ad2, push in flight; READY mails follow; Sonnet gates (tier 2).
- **E:** KS-1557 round 3 on #1654 (migration 055; Kam card a), tier 1, LAST allowed round; plan confirmation due; B2 attribution policy stops back to me if it needs more than corroboration-required; Opus delta gate after.
- Gates running now: CH1, CI1. All earlier gates returned and were verified (CA1 CB1 CC1 CD1 CE1 CF1 CG1).

## 2. KAM'S CARDS
OPEN: `secuura-ks1695-ownerless-records-who-reads-1020` (amended after Stuart's comment: rec b, default c). RULED 14:01 today, delivery owed: `secuura-ks758-erasure-log-subject-ref-1020` = c (G round 2), `secuura-ks1689-m365-failed-signin-status-1020` = d (R's KS-1689 PR), `secuura-ks1557-055-second-nogo-round3-1020` = a (E). Also delivery owed: `secuura-ks1688-org-merge-edge-which-side-1020` = a (KS-1688 fix seat posts it; waits for #1654), `secuura-m365-admin-setup-for-customer-org-1020` = b (KS-1678 future work). Mark each delivered with `decision_queue.sh --delivered ID ARTEFACT` when it sits in a PR/ticket comment.

## 3. OWED BY WEDNESDAY (in order)
1. Verdicts: CH1 (#1668, tier 2) and CI1 (#1669, tier 1): verify trailer + heads + merge-tree + stray, then GO or ruling.
2. R's comment-only commit on #1664 -> check the delta is comments only (+ the K5 title), GO the new head (no gate).
3. D 26th's two READYs -> Sonnet gates (tier 2).
4. E's plan confirmation -> confirm against its brief (B2 policy stop).
5. C's #1667 round 2 READY -> Opus gate; G's KS-758 round 2 -> Opus gate; PR 2 after PR 1.
6. Tell Kam (receipt): KS-1692 PR 2 admin status route will answer 503 after the write (ruled by me, KS-888 precedent); the CI runs with conclusion failure and zero steps on develop's own heads (C 32nd's report, cause unmeasured, for Kam/Peter); correlator disclosure from G's hash (same hash = same subject).
7. Spark: screen 22 when the gauge allows (KS-1672 only if the ticket spells out the INSERT and fieldMap write sites; auth-shaped, tier-1 gate); ks_1682_p1b/p2 not held (R's #1668 covers them).
8. STANDING_LINES line (claim via wed_claim): searchIssues returned 12 hits for a nonsense control term (G 13th, C 32nd both measured), so a hit list proves nothing.
9. Ledger rows added today by this seat: the partial read of G's mail; the self-contradictory N2 instruction. No lesson FILE edited, so no digest regeneration; do NOT commit the boot digests from a seat (two seats regenerate them and the rebase conflicts: take origin's); the 05:30 ledger archive.
