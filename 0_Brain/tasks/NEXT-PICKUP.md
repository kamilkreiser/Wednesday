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

## 1. LIVE WORK (refreshed 21:1x Sun) — panes %0 (Wednesday), %2 J 12th, %3 R 47th, both seats on Opus 5.5
- **develop = 833984fc94acf6bc00ff8e5d6642fa768dd44e09** (verified): today merged #1560, #1561, #1567, #1566, #1565, #1555 (KS-1114). Nothing deployed.
- **#1568 (KS-1612 + KS-1385 b, head 16e71610366b) NO GO round 1** — verdict 0_Brain/reference/2026-10-18_gate-pr1568/verdict.md (sha 41dc7991bc4fd6ff, recomputed): MAJ-1 cross-tenant identity rewrite via external_id = another tenant's pkey (cells XT1/XT2). DESIGN RULED 10:2xZ: (b) — migration 050's uncallable SECURITY DEFINER trigger makes external_id and pkey namespaces disjoint DB-wide; (a) not added; legacy collisions fail closed (census per box first: tasks/DEPLOY-BLOCKERS.md); only the trigger's own SQLSTATE maps to the 409; race residual; KS-1603 direct route out of scope. J is BUILDING round 2 = THE CAP; on its READY launch a tier-1 FULL Opus gate (brief like 0_Brain/reference/2026-10-18_gate-pr1568/GATE_BRIEF.md + the XT1/XT2 cross-tenant cells + the uncallable-function control + the census control).
- **Card secuura-ks1385-cert-holder-can-rewrite-issuer-fields-1018** (INF-2; rec b, default a) posted 21:1x.
- **R 47th (%3):** pushing KS-1509, KS-1613, KS-1619 p3, KS-1545 (re-anchored by R); one READY -> ONE batched gate: KS-1613 (preflight) is tier 1 => the FABLE 5.1 TRIAL (Agent model: fable) PLUS an Opus tier-1 gate on the same PRs; the rest tier 2 on Sonnet (v1.0). Then: held READYs KS-1490 (bash_patch2), KS-1619 p1 + p2 (test_only) were held 21:1x by the extended hold_ready (send to R as the next raise).
- **HELD Spark READYs waiting for a raise seat (all read at source by Wednesday):** KS-1490-TRAILINGSLASH-1, KS-1619-THREETENANT-2, KS-1619-MULTICHUNK-1, KS-1114-HIDDENSTATUSES-2 (its raise must ALSO apply + run night/briefs/ks_1114_p2/integration_T11_followup.diff against a real Postgres). Send to R after its current batch (R raised KS-1509 as #1569 at 10:17Z; its other three pushing).
- **Tooling done today:** test_only tier (arms 15/15), hold_ready test_only + bash_patch2 kinds (subagent arms 18/18; Wednesday's own re-run passed K1-K5e, K6/K7 were still running at 21:1x: log /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/59f676bc-e3a9-4b9a-8b25-64e572c78937/scratchpad/holdkinds_arms.log, scratch, may be gone). Owed: re-baseline arm 5 of hold_ready_rung34_arms.sh (pre-existing drift).

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
