---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the overnight Wednesday seat (booted 2026-10-19 23:46) at its rotation, 2026-10-20 02:3x. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1020-0233 + git.
---

# NEXT PICKUP (Tue 20 Oct, ~02:35; rotation at ~82% context, quiet hours until 06:00)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
2. Verify every merge by fetching into the cache clone at the LITERAL path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (ls-remote through it too: the default ssh identity gets "Repository not found"). Re-hash every verdict with `sed '1d;$d' verdict.md | shasum -a 256`.
3. `cockpit.sh say` takes the cockpit NAME; `pane_close.sh` takes the `%ID`.
4. **NEW TONIGHT, armed:** `send_brief.sh` REFUSES any `GO:` subject while an untracked file sits outside 0_Brain/, 5_Project_History/, local-model/, fleet/briefs_staged/ (fleet/gate_stray_check.sh, arms 9/9). Commit your own new files first, or move a gate's stray to the scratchpad quarantine. `pretooluse_no_cd.sh` now also catches `git --git-dir/--work-tree/GIT_DIR=` write verbs outside the tree (arms fleet/tests/no_cd_gitdir_arms.sh 14/14).
5. Gate briefs: clone INSIDE the session scratchpad, LITERAL paths in `git -C` (a $VAR path is refused), npm/vitest pointed INTO the clone; the GO path refuses on strays anyway.
6. In force: Kam 10-18 new-account grant (tickets, backlog, Spark max), routing v1.0, the October deploy grant EXTENDED "until further notice" (Kam 10-19 18:22:57). Gauge 54% at 02:35.

## 1. LIVE FLOOR (02:35) — develop = 0f472ec20093995381d938aca5c5380f7caf6fef (#1636). NOTHING DEPLOYED tonight.
**Merged since this seat booted, each verified by Wednesday's own fetch (11):** #1622 bc3e2e2460ff · #1626 KS-1460 4a065fb75350 · #1627 KS-1671 a66cd6a4d172 · #1628 KS-1568 390cc0a317c9 · #1629 KS-1622 88b8ceb9f304 · #1634 KS-1658 05ad5d3ac472 · #1633 **KS-1673 PR A (High, m365 org binding)** 9207fe336797 · #1630 KS-1653 da9e96ffa · #1631 KS-1639 7e01fe495 · #1632 KS-1661 09336b240721 (stack tree 29f134c4d9e5 = AT1) · #1636 KS-1671 seam 0f472ec20 (tree 3e63ccfac6b6 = AV1). Secuura merges since the 10-19 evening: 22. All `Refs`; Done = deployed + live check.
- **R 56th (%9, Opus 5.5 by Wednesday's /model at an idle prompt):** KS-1673 PR B (Teams) pushing; branch has develop merged in TWICE (never rebased), AS1's cell D in, m365 133/133, predicted landing f006888d4ae4 on 09336b240721 (re-predict: develop is now 0f472ec2). On its READY: a **tier-1 Opus gate** (Teams webhook org binding; GET must never return another org's webhookUrl; cells assert the URL string ABSENT). Then the queue in its handover (5_Project_History/2026-10-19_seatR-55th/ + R 56th's own): KS-1634 N2/N3 test-only.
- **C 27th (%8, launched on Opus 5, switched to Sonnet 5.5 by Wednesday's /model):** #1635 KS-1262 at **gate AW1** (Opus, tier 1; brief 0_Brain/reference/2026-10-20_gate-AW1-pr1635-ks1262/GATE_BRIEF.md). ⚠ AW1 is an Agent-tool sub-agent of the PREVIOUS seat: if this seat rotated before its verdict, the verdict file still lands at that path — read it, re-hash it, then GO. Then C's queue: KS-1676 widen (11 unpinned guards incl. the settled/failed pair), the documents.ts comments-only follow-up (`Refs KS-1653`, documents.ts added to C's partition), KS-1660 (READY_KS-1660-PARENTDOCDROP-1), KS-1500+KS-1468 (one test-only PR, same ks963 file).
- **Spark:** screens 15 + 16 ran 8 PASS, all held and raised/queued. Pool exhausted at screen 16 (measured WHY in spark/queue.md). Re-screen when new tickets appear (tonight: KS-1670, 1672, 1673, 1675, 1676, 1677, 1678 — mostly design or Claude-shaped).

## 2. KS-1673 (HIGH) — state
- PR A merged (9207fe336797). Live reach measured by R 55th: kintsugi m365 CONFIGURED (ENTRA_* set) with 0 connections and 0 webhooks; demo unconfigured; 0/0. Nothing was exposed; kintsugi was armed for its first connection. Kam told on the panel ("don't connect M365 on kintsugi until merged"): **tell him PR A is merged, PR B (Teams) pending, and that the fix is not DEPLOYED until a kintsugi deploy round.**
- Rulings (Wednesday's, in v1.3 scope): no admin bypass; Teams in KS-1673; two PRs; existing rows re-connect not backfill.
- Filed: KS-1675 (RLS: code says svc_m365_connections is OUT of the fail-closed flip; boxes show forced RLS but flags cannot tell fail-open from fail-closed: open), KS-1677 (callback state = bare connection id, any status, Medium; gate AS1 measured the rebind), KS-1678 (wizard sends a tenant id as organizationId, Medium).

## 3. KAM'S CARDS
- **NEW: `secuura-m365-admin-setup-for-customer-org-1020`** (open): should admin-assisted M365 setup follow his KS-1570 (b) explicit-organisation-scope model? rec/default (b); fail-closed until built. Panel line sent.
- Tuesday's Datasec cards stay Tuesday's.

## 4. OWED BY WEDNESDAY
1. **Kintsugi deploy round** under the October grant: tonight's 11 merges incl. KS-1673 PR A are on develop, nothing deployed. A READ-ONLY census seat first (DEPLOY-BLOCKERS), then a deploy seat, kintsugi first, live sweep, then demo. KS-535 wallet rule. Kam's word is not needed (grant), but flag it to him in the morning receipt.
2. fleet_ack: a QUESTION is not collected for ~2-4 min after arrival; `answered` rc 3 until then (re-run).
3. Fable 5.1 coordinator trial (routing decision 7); gate brief template should name touched services' suites as RUN or NOT-tested.
4. The 95 `t <t@e.com>`-authored commits on develop (KS-1668 tonight was another); keep every stash.
5. Secuura launcher pins `--model claude-opus-5` (Launch_Claude.command:664): every Secuura seat needs `/model` at its first idle per routing (C1 Sonnet, C3 Opus 5.5). `/model` also saves a default in that config; the launcher pin overrides it.
6. KS-1665 (deploy.sh admin fallback on a failed key-vault read) deserves more than Low before any production deploy: raise in the morning receipt.
7. Regenerate BOTH boot digests at the wrap (ledger edited tonight).
