---
date: 2026-10-18
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 18:5x Wednesday seat at its 51% checkpoint (2026-10-18 ~19:23). Replace wholesale again; never stack. Previous version: NEXT-PICKUP.md.pre-1018-1923 + git.
---

# NEXT PICKUP (Sun 18 Oct evening)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, newmail.sh (to a file, never piped), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, pane_prompt_check.sh %0, `local-model/spark/tunnel.sh check` (up if down; it was DOWN at this boot).
2. **Kam's instruction in force (EXPIRING-GRANTS top row, 10-18 ~19:0x, no expiry, tied to this account):** "new account so please work on the tickets, backlog and definition of which agent to use for what. Spark connected so give it as many tickets as it can handle". Lesson learnings/2026-10-18_new-account-tickets-backlog-routing-definition-spark-max.md. The 10-15 Spark-only and push-first rows are EXPIRED. Gauge 1%.
3. **MONDAY 2026-10-19: WED-154** storage policy (policy + dry-run + first measured report + a card; nothing removed before Kam sees it). Weekly consolidation is also due (first session after Sunday).
4. **Commit your own files BEFORE any tool that pulls** (wed_claim, safe_pull, safe_push): wed_claim's autostash swallowed today's new note at 19:1x (ledger row 10-18; stash@{0} KEPT, restored).

## 1. LIVE WORK (final block of the 18:5x seat, 22:3x Sun, written at ~85% just before rotation) — panes %0, %2 J 12th (~80%+, wrapping), %3 R 47th (~80%, rotating at its boundary)
- **develop = db9bd1602734f2f8d85aed800836e18236b4f9e3** (ls-remote 22:3x). Merged tonight and verified at source: KS-1114 #1555 + #1560 #1561 #1565 #1566 #1567 #1569 #1570 #1571 (tally in the daily note). Nothing deployed.
- **#1572 (KS-1545 step 1, head 778a610bf0afeab8475f5cebb86e8312515487b2):** GO sent (gate E1 Opus GO WITH NOTE, sha cc91eb9abeaa70f0); R running its shell leg then merging. VERIFY it at source (ls-remote develop + log) when R's MERGED lands.
- **#1568 (KS-1612 + KS-1385 b) NO GO AT THE CAP** (round 2, sha 3486a4efab9b5d1f, recomputed): MAJ-A orphan anchor_store rows (no documents row) still allow a cross-tenant identity rewrite; nothing can ship from it. HELD, J told. **Card secuura-ks1612-third-round-after-cap-1018** (rec a third round; default b hold + re-plan around KS-1384). On Kam's (a): J (or J 13th) designs first (residue options in the r2 verdict), Wednesday rules, one more tier-1 FULL Opus gate.
- **Card secuura-ks1385-cert-holder-can-rewrite-issuer-fields-1018** open (rec b, default a).
- **R's NEXT raise batch (being pushed):** KS-1114 follow-up (T11 re-pin RUN on real Postgres), KS-1619 p1 + p2 (test-only), KS-1490 (bash_patch2). On its READY: batch gate under routing v1.0 (KS-1114 p2 touches the public verify route -> tier-1 Opus; the rest tier 2 Sonnet). Follow-up ticket (KS-1621 or sibling) carries the gate D/E1/E2 notes incl. Fable's #1570 second-slash cell.
- **Routing v1.0 trial evidence:** row 1 (Fable vs Opus, gate E1) in 0_Brain/reference/2026-10-18_model-routing/EVIDENCE.md. Fable coordinator-task trial still OWED.
- **Spark:** queue empty after today's 9 rounds (8 PASS: KS-1509, KS-1490, KS-1613, KS-1619 p1-p3, KS-1114 p2 + KS-1545 to Opus). Next briefable: KS-1482, KS-1497 items 2+4, the follow-up ticket's cells. Brief them (Sonnet drafter, row C8).

## 1b. KAM 20:55 RULINGS — APPLY THEM (added 20:5x)
- **Routing v1.0 IN FORCE** (card wed-model-routing-v10-approve-1018 = a, all seven). Spec `2_Project_Files/fleet/specs/model-routing.md` swapped in; boot line changed; lesson `learnings/2026-10-18_model-routing-v10-approved-route-by-the-table.md`. Every launch receipt carries `model: <id> -- <row> -- <P1-P4> -- <gauge>`. **Tier-2 gates now on Sonnet** (Agent tool `model: sonnet`). **FABLE 5.1 TRIAL OWED:** the NEXT tier-1 gate (R's batch: KS-1613 preflight is tier 1) runs on Fable (Agent tool `model: fable`), and the same PR also gets its normal Opus tier-1 gate, so the two verdicts compare; plus one coordinator-task trial. Record both in model-routing.md section 6-style rows.
- **KS-1114 deny-list follow-up** (card secuura-ks1114-deleted-status-found-by-title-1018 = a): after #1555 merges, brief the Spark: make the hidden set case- and space-insensitive and add 'deleted' and 'expired' (the r2 gate's N1; verdict 0_Brain/reference/2026-10-18_gate-pr1555-r2/verdict.md). It is an auth-adjacent public route: row says Spark may take a spelled-out edit there with a tier-1 Opus gate.
- Tuesday told (coordination mail, 20:5x).

## 2. KAM'S CARDS OPEN
Secuura: none open (deleted-status card ruled a 20:55:56). WED: none open (routing v1.0 ruled a 20:55:59). The four 18:59-19:00 cards are ruled and reconciled. Datasec: composer-l05-setup-card-too-1014 (Tuesday's). Unanswered panel question from 10-16 (bf-f955bd7b56aa959f, lean boots at >=95%): not a rule.

## 3. OWED BY WEDNESDAY (own tools, small)
1. wed_claim.sh: refuse to autostash when anything outside dashboard/data is dirty (safe_pull's rule).
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer; `say %4 ...` (pane id) is a silent no-op: fail loudly.
3. pretooluse_no_cd.sh flags write verbs in the session SCRATCHPAD clone as "outside WEDNESDAY" (blocked a merge-tree in a scratch clone 19:0x): allow the scratchpad path.
4. Proposal for Kam (not urgent): Secuura launches default SECUURA_ALLOW_ONDISK_KEY=1 (or seed the keychain), so F-02 stops leaving a keepalive-less core.sshCommand (R 47th's preflight, verbatim, repeated it).
5. INDEX.md refresh (newest block 2026-09-23).
6. Deploy round (Kintsugi): READ-ONLY census seat first, once tasks/DEPLOY-BLOCKERS.md clears (GATEWAY_VOUCH_SECRET first).
7. stash@{0} (10-18 autostash, restored) and older stashes are KEPT, never dropped.
