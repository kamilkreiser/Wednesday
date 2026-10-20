---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 11:1x Wednesday seat at its 65% checkpoint (12:0x AEDT). Replace wholesale again; never stack. Previous versions: git history of this file.
---

# NEXT PICKUP (Tue 20 Oct, written 12:0x AEDT by the 11:1x seat)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` with the LITERAL path (a `$VAR` path is refused by the no-cd hook; wrap multi-command git in `bash <<'EOF'`). `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`. Zoom before any raw keypress.
3. send_brief/brief_and_launch need `WED_AGENT=wednesday`. Subjects never carry hold/stop/checkpoint. Send, tap and note are THREE separate calls (receiptguard refuses a note in the send's command). Push: commit own files by pathspec, `tools/safe_pull.sh`, then `git push`.
4. Every gate verdict: `sed '1d;$d' verdict.md | shasum -a 256` must equal its trailer (whole-file control differs). **BV1's did NOT reproduce** (see 1): never GO on a verdict whose hash fails.
5. In force: Kam 10-18 new-account grant, routing v1.0, the October deploy grant EXTENDED "until further notice", the TESTED merge grant, merge-and-archive grant. Gauge 74% at 12:0x (80-90 band not reached).

## 1. LIVE FLOOR (12:0x) — develop = 610570e5a75790d8ebf4264c4aec3ec8bebc0609 (#1657)
Merged today, each verified by a Wednesday fetch: #1645 #1646 #1648 #1647 #1649 #1650 #1651 #1652 #1653 #1658 #1656 #1655 #1657 = 13. **Kintsugi DEPLOYED to 89956fe92956 by D 25th** (verified from outside: /health/deep 200, startupMigrations applied 48, lastRunAt 00:47:41Z; ancestry on develop rc 0). Demo d75bfe2deb80, untouched by deploys. Notices posted: KS-772 ec36a174, KS-485 28c0ddf2 (D's ids, byte-equal to drafts).
- **GATES RUNNING (Agent, background):** **BW1** (Sonnet, tier 2) = #1660 KS-1682 BR1 residue (R 59th, head 1400219cf2b8, test-only), brief `0_Brain/reference/2026-10-20_gate-BW1-pr1660-ks1682-br1/GATE_BRIEF.md`. **BX1** (Opus, tier 1, RAISED) = #1659 KS-1659 (G 12th, head 97eaffe0d300): BV1 said GO WITH NOTE but its hash fails and it found a possible NEW same-tenant read reach on a NULL-owner row (documentRepo.ts:176 + documents.ts:1124); BX1 drives it on real PG. Brief `0_Brain/reference/2026-10-20_gate-BX1-pr1659-ks1659-tier1/GATE_BRIEF.md`. If BX1 confirms new reach: round 2 of 2 to G with its remedy options; else GO.
- **#1654 KS-1557: BU1 NO GO at round 2 of 2 -> CARD `secuura-ks1557-055-second-nogo-round3-1020`** (rec a round 3 corroboration-required; default c HOLD). C 31st wrapped. On a tap of (a): launch a C seat for round 3 (C 31st's handover `!CODING/Secuura/Blockchain/5_Project_History/2026-10-20_seatC-31st/HANDOVER.md` carries B2, N1-N7 and the round-3 shape), then an Opus delta gate; on (b): a read-only kintsugi count first. KS-1688's fix waits for #1654 to MERGE.
- **R 59th (%21, still claude-opus-5; Sonnet switch owed at a ZOOMED idle, two attempts found it busy):** #1660 at BW1; item 2 logger PR next (also pins `e.secret !== ''`, ruled), then BP1 NB1/NB2, then KS-1687 plan + KS-1689 options (-> a card for Kam with a default).
- **G 12th (%20, ctx ~70%):** KS-1558 next, then KS-758 on default (b) (card `secuura-ks758-erasure-log-subject-ref-1020` with Kam, rec c), then the BT1 N1 test-only PR (X1/X2/X3 cells). #1659 not GO until BX1.
- **D 25th (%17, ctx ~53%):** demo key_66e82ef0 revoke APPROVED narrowed (demo@secuura.io only; 403 -> STOP; witnesses: is_active false, activeApiKeys 42 -> 41, control /auth/me + key_61774985), then wrap. On its report: tell Kam, `decision_queue.sh --delivered secuura-demo-smoke-key-revoke-after-measure-1020 "<artefact>"`, verify wrap on disk, score, pane_close.
- **C lane EMPTY by decision** (both items wait on Kam's card). Scored today: R 58th 0.92, C 31st 0.88.
- **Spark:** pool exhausted per SCREEN_20; a deeper screen or new tickets needed. Ornith idle: accepted (Kam 10-09).

## 2. KAM'S CARDS
- OPEN (Secuura): `secuura-ks1557-055-second-nogo-round3-1020` (rec a, default c hold), `secuura-ks758-erasure-log-subject-ref-1020` (rec c guarded hash, default b category-only). Both on the panel with lines.
- Ruled, delivery OWED: smoke-key revoke (D running it); `secuura-ks1688-org-merge-edge-which-side-1020` = a (the KS-1688 fix seat posts it); `secuura-m365-admin-setup-for-customer-org-1020` = b (KS-1678 future work).
- fleet_ack: answered R59 plan, G12 KS-758; D25 revoke question NOT yet collected (re-run `fleet_ack.sh answered "demo key_66e82ef0 revoke" "D25 revoke"`).

## 3. OWED BY WEDNESDAY (in order)
1. BW1 / BX1 verdicts -> hash check, own merge-tree on live develop, GO or round.
2. D 25th's revoke report -> Kam told, card delivered; D wrap -> verify, score, close.
3. Kam's taps on the two open cards -> act per section 1.
4. R 59th: Sonnet switch at an idle; KS-1689 options -> card.
5. Fable 5.1 coordinator trial (routing decision 7) still OWED.
6. At the wrap: regenerate BOTH digests only if a lesson FILE was edited (none today: ledger only); the 05:30 ledger archive.
