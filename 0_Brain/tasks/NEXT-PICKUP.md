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

## 1. LIVE WORK (19:2x Sun) — panes %0 (Wednesday), %2 J 12th, %3 R 47th
- **develop = d0c5d2e0ef8bf8c1e70f9684503c5fb3a3e53c4f** (Peter merged his own #1562-#1564, systemTest, over the weekend; 0 overlap with ours).
- **GATE C** (Opus background subagent of the Wednesday seat that launched it): #1560 (KS-1543 p2+3, 180c7c82) + #1561 (KS-1462 i1, ba8c1879). Verdict -> 0_Brain/reference/2026-10-18_gate-C-pr1560-pr1561/verdict.md. On GO: recompute sha (line 3 deleted), ls-remote the heads, mail the R LANE a head-bound GO per PR (one at a time). If this seat rotated, the subagent died with it: re-launch from the same GATE_BRIEF.md.
- **Seat J 12th (%2)**: KS-1114 existence-only fix on #1555 (round 2 of 2) then KS-1385 (b) + KS-1612. Brief fleet/briefs_staged/2026-10-18_seatJ12_ks1114_fix_ks1385b_ks1612.md. Its plan confirmation not yet answered at 19:23. **Still on Opus 5: switch to claude-opus-5-5 at its first idle (idle check in its own call, then /model, then Enter on the dialog, then tell it in the ANSWER).**
- **Seat R 47th (%3)**: on Opus 5.5 (switched 19:2x). Plan CONFIRMED (ANSWER 08:22Z): waits for gate C GO; then KS-1541 + KS-724 as two PRs in one batched gate; KS-1614 after #1560 merges; team-notify comments (KS-772 Stuart, KS-485 Peter) after merges. Brief fleet/briefs_staged/2026-10-18_seatR47_merge_gateC_raise_1541_1614_ks724.md.
- **Background subagents (die with this seat on rotation; check their outputs on disk first):** Spark screen + brief-writer + rounds -> 0_Brain/reference/2026-10-18_spark-screen/SCREEN.md (it does NOT hold PASSes: Wednesday reads every PASS at source and holds it); test_only tier wiring -> spark/round.sh + brief_lint.py with .pre-1018-testonly backups + an IMPROVEMENTS row (claimed in wed_claim; commit it after reading the arms); model-routing v1.0 draft -> fleet/specs/model-routing.md.v1.0-draft + summary 0_Brain/reference/2026-10-18_model-routing/SUMMARY.md (claimed; review, swap in, publish the summary to Kam as a short doc with decisions + defaults). models_latest.json now lists a Fable level (claude-fable-5-1): a routing question for Kam, not assumed.

## 2. KAM'S CARDS OPEN
Secuura: none (all four ruled 18:59-19:00 and reconciled). Datasec: composer-l05-setup-card-too-1014 (Tuesday's). Unanswered panel question from 10-16 (bf-f955bd7b56aa959f, lean boots at >=95%): not a rule.

## 3. OWED BY WEDNESDAY (own tools, small)
1. wed_claim.sh: refuse to autostash when anything outside dashboard/data is dirty (safe_pull's rule).
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer; `say %4 ...` (pane id) is a silent no-op: fail loudly.
3. pretooluse_no_cd.sh flags write verbs in the session SCRATCHPAD clone as "outside WEDNESDAY" (blocked a merge-tree in a scratch clone 19:0x): allow the scratchpad path.
4. Proposal for Kam (not urgent): Secuura launches default SECUURA_ALLOW_ONDISK_KEY=1 (or seed the keychain), so F-02 stops leaving a keepalive-less core.sshCommand (R 47th's preflight, verbatim, repeated it).
5. INDEX.md refresh (newest block 2026-09-23).
6. Deploy round (Kintsugi): READ-ONLY census seat first, once tasks/DEPLOY-BLOCKERS.md clears (GATEWAY_VOUCH_SECRET first).
7. stash@{0} (10-18 autostash, restored) and older stashes are KEPT, never dropped.
