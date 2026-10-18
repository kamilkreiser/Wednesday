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

## 1. LIVE WORK (refreshed 20:2x Sun at the 65% checkpoint) — panes %0 (Wednesday), %2 J 12th, %3 R 47th, both seats on Opus 5.5
- **develop = d2ec786e6130c7ce13384185c84cc1e7566d77cb**: #1560 (36c77dc9) + #1561 (d2ec786e) MERGED on gate C, verified at source (tree 21568b66 = prediction). Nothing deployed. KS-1619 filed (gate C notes) and sent to the Spark screen agent.
- **GATE #1555 r2** (KS-1114, head 986732cf5f70de4417a76b3d2100a57bc8fe0d04, tier 1 FULL, ROUND 2 OF 2 = the cap): Opus background subagent; verdict -> 0_Brain/reference/2026-10-18_gate-pr1555-r2/verdict.md (sha on line 2). On GO: recompute, ls-remote, head-bound GO to the J LANE. On NO GO: the cap — ship closed instances, ticket the residue, a third round needs Kam. Card secuura-ks1114-deleted-status-found-by-title-1018 open (default a: merge as built, Spark follow-up hides 'deleted').
- **GATE D** (#1566 KS-1541 3697013868483a28c2da99169b5c8cdd4aef2427 tier 2; #1565 KS-724 47ca56213b6eb7b34d30fd91aea411478f33d9b1 tier 3; #1567 KS-1614 09de80685fb6b0945cae4908723d67e6a10c76ce tier 3): Opus background subagent; verdict -> 0_Brain/reference/2026-10-18_gate-D-pr1565-pr1566-pr1567/verdict.md (sha on line 4). On GO: head-bound GO per PR to the R LANE (one at a time; develop may have moved for #1555).
- **Seat J 12th (%2)**: after #1555, KS-1385 (b) + KS-1612 built + green locally (guard resolves external_id then primary key, tenant-bound; certification rows have no external_id) — READY (Opus tier 1) to come. Title shape ruled 08:3xZ: hit = {verified:false, checks:{documentExists:true}}.
- **Seat R 47th (%3)**: waiting for gate D's GO.
- **Background subagents (die with this seat on rotation; re-launch from the GATE_BRIEF files):** the two gates above; the Spark screen + brief-writer + rounds (report 0_Brain/reference/2026-10-18_spark-screen/SCREEN.md; it does NOT hold PASSes — Wednesday reads and holds; KS-1619's three parts added to its list).
- **DONE this seat:** test_only tier wired + committed (arms 15/15, claim released); model-routing v1.0 draft committed (fleet/specs/model-routing.md.v1.0-draft, NOT swapped in) + Kam's doc "Which agent does what (v1.0)" https://claude.ai/code/artifact/b5262ba7-a5a1-468e-bb36-51fa4c7e5e90 + card wed-model-routing-v10-approve-1018 (default c: stays a draft). On his ruling: swap the file in, change the boot line (Launch_Wednesday.command MODEL CHOICE override) only on (a)/(b), release the claim.

## 2. KAM'S CARDS OPEN
Secuura: secuura-ks1114-deleted-status-found-by-title-1018 (default a). WED: wed-model-routing-v10-approve-1018 (default c). The four 18:59-19:00 cards are ruled and reconciled. Datasec: composer-l05-setup-card-too-1014 (Tuesday's). Unanswered panel question from 10-16 (bf-f955bd7b56aa959f, lean boots at >=95%): not a rule.

## 3. OWED BY WEDNESDAY (own tools, small)
1. wed_claim.sh: refuse to autostash when anything outside dashboard/data is dirty (safe_pull's rule).
2. cockpit.sh say --mail: stamp the mail's own timestamp into the pointer; `say %4 ...` (pane id) is a silent no-op: fail loudly.
3. pretooluse_no_cd.sh flags write verbs in the session SCRATCHPAD clone as "outside WEDNESDAY" (blocked a merge-tree in a scratch clone 19:0x): allow the scratchpad path.
4. Proposal for Kam (not urgent): Secuura launches default SECUURA_ALLOW_ONDISK_KEY=1 (or seed the keychain), so F-02 stops leaving a keepalive-less core.sshCommand (R 47th's preflight, verbatim, repeated it).
5. INDEX.md refresh (newest block 2026-09-23).
6. Deploy round (Kintsugi): READ-ONLY census seat first, once tasks/DEPLOY-BLOCKERS.md clears (GATEWAY_VOUCH_SECRET first).
7. stash@{0} (10-18 autostash, restored) and older stashes are KEPT, never dropped.
