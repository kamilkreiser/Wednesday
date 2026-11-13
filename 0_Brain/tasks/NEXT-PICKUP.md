---
date: 2026-11-13
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's.
status: live
supersede: REPLACED WHOLESALE 2026-11-13 12:1x by the 11:5x seat at its 50% checkpoint (the old file had grown to 264 KB of stacked blocks). The old file is kept, unchanged, at 0_Brain/tasks/NEXT-PICKUP.md.pre-1113-1215-wholesale (also in git at 80d89f162e). Replace wholesale; never stack: add ONE block at the top per checkpoint, and fold older blocks away at each rotation.
---

# NEXT PICKUP, Fri 13 Nov 2026 (Mac mini seat)

## CHECKPOINT 12:1x 13 Nov, the 11:5x seat (ctx 50%) - READ FIRST
- **develop a288aa45d6b2** (PR 2226's squash, merged 01:04:58Z; gh api + Wednesday ls-remote 12:06:15). Merges today: 2147, 2144, 2141, 2137, 2125, 2134, 2126, 2226 (8).
- **PUSH FREEZE, still on:** pre-push audit legs 6/7 refuse every push on three `hono` 4.13.13 advisories (GHSA-4m76-xfj5-7975, GHSA-h7mg-cq63-vhpq, GHSA-3gg2-335m-rxc6) plus two GitHub-only ids (GHSA-46wx-v44x-9hh2, GHSA-4h7h-rv7c-7m2v; Wednesday read both at api.github.com: patched 4.13.16). MERGES are not affected (B 172nd measured: `gh pr merge` via API, no pre-push leg; one row's measurement).
- **FLOOR:**
  - %204 **Seat S 78th** (FIX -S, Sonnet 5.5 confirmed on its statusline 12:14): the hono 4.13.13 -> 4.13.18 refresh in the root lock + services/mcp-server lock. Brief STAMPED 12:0x: fleet/briefs_staged/2026-11-13_seatS78_hono_core_lock_refresh.md (sent + verified 01:07:32Z). Rulings: base a288aa45d6b2; seven ids; 4.13.18 accepted; the seat files its own ticket; TIER 1; proof 6 dropped. Plan ANSWERED 01:19:15Z (GO to start; rung 6 met). STATUS 1 01:24Z: commit e29f8e8fa4b6 (KS-2195, P1, filed by the seat), AFTER proof green, hooked push RUNNING (13-25 min). **READY 01:39Z: PR 2227, head e29f8e8fa4b6. GATE 350 RUNNING (Opus, background; commissioned 12:40 from reference/2026-11-13_gate350-tier1-ks2195-hono/commission.md: RE-COMMISSION from it if verdict.md is absent after a rotation). Spark F24 numstat MATCH. NEXT = verdict + Spark numstat filler -> ADDENDUM to the B seat inserting it -> GO -> MERGED -> ls-remote -> mail Seat R 118th 'GO: re-push row 58 (Seat R 118th)' + tap -R.**
  - %192 **Seat R 118th** (FIX -R, KS-1699, head 5ca0ef71a3d4 local, NOT on origin): HOLDING until S 78th's PR merges. Its re-push grant (OVL_IGNORE_PRS=2160 + CENSUS_ACCEPT certifications.ts=2160) is in fleet/briefs_staged/2026-11-13_R118_answer_audit_block.md. After its push: READY FOR GATE (tier 1) -> Opus gate (shape reference/2026-11-13_gate348-tier1-pr2224-2225/commission.md) -> merged BEFORE PR 2225.
  - **Seat B 172nd WRAPPED** 01:11Z, scored 0.95, pane %201 closed. Its record: !CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatB-172nd/HANDOVER.md.
  - %207 **Seat B 173rd** (MERGE -B, Sonnet; brief fleet/briefs_staged/2026-11-13_seatB173_merge.md STAMPED 12:1x; sent + verified 01:16:36Z). ORDER (stamp): 2097, 2096, 2095, 2090, then 2098, 2089, 2079 t1, 2220-2223, 2224 t1; S 78th's PR by ADDENDUM. GOs use the kit's FIXED squash form `QA gate <verdict>; merge GO pinned to <head12>.` NEXT MAIL = its plan QUESTION -> ANSWER (model fleet/briefs_staged/2026-11-13_B172_answer_plan.md) -> READY 2097 -> GO (model 2026-11-13_B172_go_2226.md minus the title ruling; gate 264 line 1 at source; ls-remote in the send action) -> MERGED -> next row.
- **Kam:** two rulings today, both 07:52 (premerge nine = c; morning plan = a). Nothing since. reconcile: 0 to rule. Stale cards: 0.
- **Usage 96%** (a guide, Kam 2026-10-22). Only repo-write seats (merge, fix) launched. Spark IDLE since 11-11 (o162-o164 screens all stopped on open-PR overlaps); its next work = the numstat fillers on S 78th's and B 173rd's READYs.
- **Gate commissions are Agent-tool subagents and die with a rotation:** re-commission from their commission.md if verdict.md is absent.

## OWED (in order, after the floor)
1. The floor items above.
2. **Weekly consolidation LAPSED since 10-19** (skills/weekly-consolidation.md). Promotion candidates waiting: (a) a PreToolUse advisory on unbounded listings (ledger 13 Nov, w=3 today); (b) advisory on `<script>.sh --help`; (c) a checkpoint check that a wed-morning-plan-<MMDD> card exists after 09:00; (d) brief_and_launch refusing a bare 'Secuura/Blockchain' and reading back by message id; (e) wed_push.sh (store-safe push, w=3 11-11).
3. INDEX.md refresh (not done 11-11 to 11-13). fleet_ack collector stale ('answered' refuses on no subject match).
4. KS-2173 part 2; G328-2207-6; the board-seat filing list (B 170th / 171st / 172nd / S 77th wraps add to it).
5. **The 11-11 OWED list (R 95th advisory card, S 55th/B 133rd, o138 passes, R 96th, CLAUDE-BUILD lanes) is NOT carried as live:** most rows are two days old and unverified here. Before acting on any of them, read the item in NEXT-PICKUP.md.pre-1113-1215-wholesale (bottom section 'OWED') and re-measure it at source.

## STANDING (unchanged; the lessons carry the detail)
- Board grant (Kam 11-06 / 11-11): clear the Secuura board, In Progress + Backlog, Spark as much as possible, as many agents as the code partition allows; outer read Fri 2026-11-20. Demo FROZEN. Peter/Stuart tickets stay theirs.
- Merges on Wednesday's head-pinned GO after a QA gate (TESTED grant); no 'do not merge' self-hold sentence in our PR bodies (card secuura-premerge-block-nine-prs-1113 = c).
- Every GO subject is the seat's requested subject, copied; every --to is copied from the previous send receipt for that lane.
