---
date: 2026-10-22
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the Opus 5.5 Wednesday morning seat of 22 Oct at its 66% checkpoint (2026-10-22 15:51 AEDT). Replace wholesale again; never stack. Previous version: NEXT-PICKUP.md.pre-1022-1552 and git history.
---

# NEXT PICKUP (Thu 22 Oct, written 2026-10-22 15:51 AEDT; ctx 66%, weekly 7d 91%)

## 00. LIVE NOW
- **Seat D 29th, pane %29 (Secuura/Blockchain-D, Opus, row C6):** deploying develop `bcc51903d89329932532058cbd58fd1ced7d3a0c` to KINTSUGI (kintsugi runs 32964477fe88), then posting Kam's ruled comments. Brief: `2_Project_Files/fleet/briefs_staged/2026-10-22_seatD29_kintsugi_tip_and_posts.md`. Launch VERIFIED (rung 6: its plan confirmation 04:48Z). Evidence root: `!CODING/Secuura/Blockchain/5_Project_History/2026-10-22_seatD-29th/`. Stamp pre-20261022d1; batched build (two per invocation, load gate 6); no migrations in the delta (my read; the seat proves its own). Expected mails: STATUS Phase 0, STATUS build, DEPLOYED, POSTED, wrap. On DEPLOYED: re-measure kintsugi from outside myself (/health/deep, an unknown /api route 404), then tell Kam. Then demo may follow kintsugi under the October grant (a later deploy seat).
- **DRAFT 4 (Peter, KS-485): posts as ruled** after Part A. **DRAFT 1 (Stuart, KS-1557): WAITS for Kam's card `secuura-ks1557-draft1-overtaken-by-stuart-1022`** (rec b = delete three overtaken lines, add nothing; default = not posted). The seat prepares `drafts_1b.md` and mails me the diff: CHECK IT IS DELETIONS ONLY before any GO. On b: GO to post 1b; a: post DRAFT 1 verbatim; c / no tap: nothing for KS-1557. My ANSWER 04:50:14Z carries these rules.
- Stuart's 23:30Z comments (read by D 29th): KS-1709 fd04f154 (cause = S's malformed DID, his PS-1324), KS-1557 ba2aa2b2 (his "verified end to end" narrowed to route level), KS-772 e6f64263 (uat-ps AnchorIdentity false until PS-1324; dev-ps loses anchors on kintsugi today: pre-existing, S's).

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

## 3. BOARD
KS open 688 at 06:0x (Backlog 352, Todo 26, In Progress 267, In Review 40, Blocked 3; split by state/priority because two states exceed a 250 page). 10-12 baseline 509; 239 created vs 74 closed since 10-12 (closed includes 70 archived; includeArchived read). The 31 Oct target is off track; told Kam.

## 4. KAM'S CARDS
OPEN: `secuura-ks1557-draft1-overtaken-by-stuart-1022` (rec b). Ruled today: ks1707 = a, ks1557 (original) = a, deploy-tip-kintsugi-and-post = a. Datasec cards are Tuesday's.
