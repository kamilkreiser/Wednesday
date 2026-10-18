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

## 1. LIVE WORK (refreshed 20:4x Sun at the 70% checkpoint) — panes %0 (Wednesday), %2 J 12th, %3 R 47th, both seats on Opus 5.5
- **develop was d2ec786e6130c7ce13384185c84cc1e7566d77cb at 20:4x** (#1560 + #1561 merged and verified). Re-read it: merges are in flight.
- **GO SENT, merging now (verify each at source with ls-remote + log + tree):**
  - J LANE: #1555 KS-1114 at 986732cf5f70de4417a76b3d2100a57bc8fe0d04 (tier-1 gate r2 GO WITH NOTE, sha bea8745916286da7).
  - R LANE, in order: #1567 KS-1614 at 09de80685fb6b0945cae4908723d67e6a10c76ce, then #1566 KS-1541 at 3697013868483a28c2da99169b5c8cdd4aef2427, then #1565 KS-724 at 47ca56213b6eb7b34d30fd91aea411478f33d9b1 (gate D, sha dacec9e78fccfe6e).
  - R files a gate-D follow-up ticket (info.ts:131 length bound, 'refused' wording, mutants H1-M3/M8) for the Spark.
- **J 12th next:** KS-1385 (b) + KS-1612 push retry (head 16e71610366b), then READY -> a tier-1 FULL Opus gate (anchored-identity authority rule). Brief it like 0_Brain/reference/2026-10-18_gate-pr1555-r2/GATE_BRIEF.md.
- **SPARK held READYs (read at source by Wednesday, TREE-IDENTICAL to goldens), waiting for a raise seat:** night/READY_KS-1509-NULLHEIGHT-1_..., READY_KS-1613-DENOMABORT-1_..., READY_KS-1619-DESCRIBER-3_... . Three more read and correct but REFUSED by hold_ready (KS-1490 bash_patch2; KS-1619 p1 + p2 test_only): a tooling subagent is extending hold_ready (arms first, then holds them with bare ROWIDs TRAILINGSLASH-1, THREETENANT-2, MULTICHUNK-1); if this seat rotated, it died: re-commission from the spark-screen report. **KS-1545:** counter spent (two A2a fails, code correct) -> Opus on the next open Claude seat (re-anchor the hunk headers). **Next briefable:** KS-1482, KS-1497 items 2+4; the KS-1114 deny-list follow-up once Kam's card rules (default a).
- **Raise plan for the held READYs:** one raise seat (R lane after its merges, or R 48th) takes KS-1509, KS-1613, KS-1619 p1-p3, KS-1490 (+ KS-1545 by Opus) as file-disjoint PRs, gated in batches.
- **DONE this seat:** test_only tier wired (arms 15/15); model-routing v1.0 draft + Kam's doc https://claude.ai/code/artifact/b5262ba7-a5a1-468e-bb36-51fa4c7e5e90 + card wed-model-routing-v10-approve-1018 (default c).


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
