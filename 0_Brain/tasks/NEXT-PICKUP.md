---
date: 2026-10-22
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the Opus 5.5 Wednesday morning seat of 22 Oct at its 66% checkpoint (2026-10-22 15:51 AEDT). Replace wholesale again; never stack. Previous version: NEXT-PICKUP.md.pre-1022-1552 and git history.
---

# NEXT PICKUP (Thu 22 Oct, written 2026-10-22 15:51 AEDT; ctx 66%, weekly 7d 91%)

## 00. STATE AT 22:1x (refreshed after D 29th's wrap)
- **Floor: wednesday %0 + fleet-monitor %1 only.** D 29th wrapped 11:09Z, scored 0.92, pane %29 closed (listeners 30 -> 30). HANDOVER `!CODING/Secuura/Blockchain/5_Project_History/2026-10-22_seatD-29th/HANDOVER.md` (30,178 B), its §10 is tomorrow's list.
- **KINTSUGI runs develop bcc51903d893** (deployed ~20:34 AEDT 22 Oct; verified from outside by Wednesday). Rollback set pre-20261022d1. NSG AllowSSHFromDev now 157.211.44.146/32 (rollback 157.211.46.215/32). **DEMO still runs 32964477fe88.**
- **OPEN, KAM'S: card `secuura-kintsugi-deploy-notice-1022`** (rec a: post K1b to Stuart on KS-772; nothing to Peter). K1b = `.../2026-10-22_seatD-29th/evidence/draft_K1b.txt`, 1,114 B, sha16 60cfbc6beaab9c8b, PRE-CHECKED by Wednesday (character subsequence of K1; only the 'If the ruling goes that way' sentence removed). On his tap a: the next Secuura seat posts it verbatim (pre-send hash gate, absent-id control, mention node). Default: nothing posted; raise it in the morning receipt.
- **TOMORROW, Wednesday's plan (the daily workload is mine):** (1) DEMO deploy of bcc51903d893 by a fresh Opus deploy seat after kintsugi's overnight soak: D 28th's method on demo's 2 vCPU / 3.9 GB, batch <=2 with the load gate, DEMO's swap_one orientation with the blank-mnemonic arm reordered, KS-535 demo hashes; that seat also posts K1b if Kam has tapped. (2) KS-1707 seat (ruled a). (3) One Sonnet raise seat for the three held Spark passes. (4) The Secuura launcher's box-reachability preflight leg as a brief item.
- Cards delivered today: ks1557 (both), deploy-tip-kintsugi-and-post, kintsugi-ssh-rule. ks1707 ruled a, NOT yet delivered (needs its seat).

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says (by-tier digest ~623 KB: read in ~700-line chunks; the Read tool caps each call). This seat booted on **Opus 5.5** (statusline), so the launcher's `--model opus` fix is verified.
2. Then `tools/kam_rulings_today.sh`, `reconcile_rulings.py` (report, then --apply), `tools/newmail.sh`, `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'`.
3. Literal paths for `git -C`; send / tap / note are three separate calls; subjects never carry hold/stop/checkpoint; a send_brief body needs a `SELF-CHECK:` line stamped with `date`; zsh traps (no bare '=====', no PIPESTATUS).
4. **reconcile_rulings.py skips a live tap on a HASHED card id** (`card-<sha256(id)[:20]>`, long ids): rule those by hand (`decision_queue.sh rule <id> <key>`). Tool fix OWED.
5. safe_pull refuses on the regenerated boot digests: stash them by pathspec, pull, pop; on a conflict take HEAD's copy (generated files; the stash is kept).

## 1. IN FORCE (read the files, not this list)
- **Kam 2026-10-22 15:34:23: usage is a GUIDE, never a stop; route by the learnings; when unsure post a fleet-activity card and keep going; Wednesday owns the daily workload** -> `learnings/2026-10-22_usage-is-a-guide-outcomes-over-rules-route-by-learnings.md`. `fleet/USAGE_STOP.wednesday` = 100 (both branches proven). Past 70%: lean on Sonnet and the Spark.
- Routing v1.0 (`fleet/specs/model-routing.md`, every receipt names the row); October deploy grant until further notice (kintsugi first, then demo; KS-535); TESTED merge grant; merge-and-archive grant.
- Tuesday was briefed on allocation (Kam 15:35:07), verified in her inbox 04:40:06Z. Otherwise no mail to Tuesday unless Kam asks.

## 2. HELD / OWED, IN ORDER
1. **KS-1707 audit rows (Kam ruled a, 07:13:32):** re-date braces, sprintf-js and both react-router rows in `Blockchain/Dev/scripts/audit/audit-baseline.json` to 2026-11-30 under the 10-05 board-tap grant; fix deepmerge-ts forward (@prisma/config 7.10.1 depends on deepmerge-ts 8.0.2, measured at the registry 06:0x) and postcss-selector-parser (fixed in 7.1.6); remove the 15 stale rows. ONE Sonnet seat (row C1/C2), then a QA gate. **Before 2026-10-31.** Card `secuura-ks1707-redate-four-unfixable-audit-rows-1022` NOT yet delivered: deliver on the merged PR.
2. **Held Spark passes, ONE Sonnet raise seat (row C1):** `night/READY_KS-1622-LATERWINDOW1622-1_...`, `night/READY_KS-1709-KS-1709-REFUSALLOG1709-1_..._2026-10-22.diff.md` (issue route), `night/READY_KS-1709-KS-1709-RECERTLOG1709-2_..._2026-10-22.diff.md` (recertify route). The two KS-1709 passes both insert one manifest line after the ks1679 line in `ks1293-originate-suite-is-hermetic.test.ts`: the raise seat orders them alphabetically. KS-1709's kept-row half is a product decision (card it when raising).
3. **C 33rd (KS-1695 gap 2, option b ruled twice):** a build seat (Opus, row C3: access design). Brief material in the 2026-10-20 seatC-32nd records + the 04:12Z ANSWER set; plus the comment-only hunk correcting the merged R18 comment (platform_admin is NOT gateway-only).
4. **KS-1692 PR 2** (from `5_Project_History/2026-10-20_seatG-13th/HANDOVER.md`) and **KS-1688 org-merge** (card a): build seats.
5. **Stuart's KS-1557/KS-772 box asks** are now "welcome but no longer load-bearing" (his 23:30Z words); DRAFT 1 carries the answers if Kam rules a or b.
6. **Demo** after kintsugi is verified: a deploy seat, D 28th's batching method (demo is 2 vCPU / 3.9 GB).
7. STANDING_LINES additions OWED (claim first): searchIssues nonsense-term control; landing figure expected unless base moved; send_brief 'sent:' is not delivery; comments-only needs a known-unequal pair; a waiter must be a background JOB whose exit re-invokes the seat.
8. Fable 5.1 trial gate still OWED (routing v1.0 item 7).
9. Clones left in deploy-clones (G 14th's seatG14, C 32nd's, D 26th/E): Kam's drive-hygiene rule: ask later.

10. **Kintsugi SSH drift, two halves (D 29th's finding, 22 Oct):** (a) CHEAP, no Kam decision: a boot preflight leg in the Secuura launcher (`nc -z -w 5 20.198.226.148 22`; on failure print the current AllowSSHFromDev prefix and the seat's own public IP as an F-xx line). The launcher is the project's file: put it in the next Secuura seat's brief as an item, never edit it from here. (b) EXPENSIVE, Kam's (money): a stable route (Azure Bastion, a jump host, or `az vm run-command`). Card it ONLY after measuring the price from Azure's own pricing page in the same action; the cost is unmeasured today.

## 3. BOARD
KS open 688 at 06:0x (Backlog 352, Todo 26, In Progress 267, In Review 40, Blocked 3; split by state/priority because two states exceed a 250 page). 10-12 baseline 509; 239 created vs 74 closed since 10-12 (closed includes 70 archived; includeArchived read). The 31 Oct target is off track; told Kam.

## 4. KAM'S CARDS
OPEN: `secuura-ks1557-draft1-overtaken-by-stuart-1022` (rec b). Ruled today: ks1707 = a, ks1557 (original) = a, deploy-tip-kintsugi-and-post = a. Datasec cards are Tuesday's.
