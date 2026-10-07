---
date: 2026-10-07
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-07 05:3x by the night seat c1dbe0b9 (booted 01:5x) at the 05:30 shift-change wrap, ctx ~63%. Previous copy in that session's scratchpad. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order) — the 06:00 MORNING seat
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. **TWO CARDS OPEN WITH KAM, both block work, lead the morning brief with them:**
   - **`secuura-advisory-freeze-3-ghsa-1007`** (filed 05:0x). EVERY Secuura push is frozen by pre-push legs 6/7 on three newly published advisories that are develop's: shell-quote GHSA-pqg4-j6r4-53mv CRITICAL; @modelcontextprotocol/sdk GHSA-6qxp-vccf-f47h HIGH (services/mcp-server); pbkdf2 GHSA-477h-4r7f-fvrx moderate (frontend/issuer, packages/shared, services/anchoring). Rec (a): one dependency seat does an in-range lock refresh, gated T1, merged first (the shape Kam ruled (a) on 10-06's five-advisory card). (b) baseline all three. (c) hold until the renewal. **Default: nothing baselined, bumped or pushed.** Wednesday's 2026-09-09 advisory grant does NOT cover it (high/critical; pbkdf2 is in shipped trees). On (a): the dependency seat's brief carries R 5th's four-way proof (in `fleet/briefs_staged/2026-10-07_seatR5_ctx_preB5.txt`) and the 10-06 card's (a) text as the shape; runtime reach of shell-quote and the MCP SDK is UNMEASURED and is item 0 of that seat.
   - **`secuura-demo-disk-retire-old-rollback-sets-1007`** (filed 01:4x). Rec (a): delete demo's `rollback-2026-09-03` + 4 small sets, KEEP `pre-20260910`, tag a fresh set first, then deploy. **Default: nothing deleted, no demo deploy.** **D 13th WRAPPED COLD at 05:3x** (0 writes to demo; scored 0.96; pane closed). On (a): brief and launch **Seat D 14th** from `5_Project_History/HANDOVER-seatD13-demo-deploy.md` (sha256/16 077d2879ec4dff8b, its READ THIS FIRST + Wednesday's rulings logged verbatim) and the D 13th brief `fleet/briefs_staged/2026-10-07_seatD13_demo_deploy.md`. Its GO subject is `GO (Seat D 14th): deploy d75bfe2deb80 to demo`, the body naming the card and the exact sets (rollback-2026-09-03 + rollback-2026-08-27-ks661, pre-ks488, rollback-20260901-prefix, pre-ks719; KEEP pre-20260910 + the new pre-<stamp>). It RE-MEASURES free space before Phase 0. On (b): re-run `boot/disk_forecast_d13.py` with the new F0. On (c): nothing. The advisory freeze does NOT block it (it deploys an already-merged develop).
1. `inbox_digest.sh --inbound` WHOLE, + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER. Bodies are fetched by message id and saved to `fleet/briefs_staged/`.
2. **Morning ticket sweep + receipt** (the standing grant). Value first: kintsugi deployed + swept at d75bfe2 (night of 10-06); gate71 GO; the #1404 merge-in built and verified, held by the freeze; the KS-1436 ticket filed.

## 🔴 LIVE STATE — LATE-MORNING SEAT (booted 11:13 2026-10-07; 51% checkpoint 11:29) — READ BEFORE THE MORNING BLOCK BELOW (items 1 and 3 there are DONE)
- **%77 Seat R 7th (`Secuura/Blockchain-R`)** LAUNCHED 11:17 (00:17:00Z verified) from `fleet/briefs_staged/2026-10-07_seatR7_merge1398_raise3to5.md` (send amendment rules Q-REBUILD7 a, Q-COVER7 adopted with the 06 pin accepted BY NAME, Q-XFER7/Q-BASE7 yes, Q-GATE7 at READY). Its 00:26Z QUESTION (boot pull ran before it read the brief; 3 ref writes = ff of develop refs to the true tip) RULED (a) 00:27Z: transfer DISCHARGED, re-baseline `rev-parse --all` at sha16 45e4418378f83e7e, no restore. **NEXT from it: plan confirmation → Wednesday's ANSWER → then the GO as a SEPARATE mail** from `fleet/briefs_staged/2026-10-07_seatR7_GO_1398_DRAFT.md` (fill the PLAN CONFIRMED readings + pane ctx; the 06-pin line is ruled ACCEPTED; strip the DRAFTER NOTES; composed docs are placed and verified). Actions verdict later by ADDENDUM after its push.
- **%78 Seat D 15th (`Secuura/Blockchain-D`)** LAUNCHED 11:28 (00:28:21Z verified) from `fleet/briefs_staged/2026-10-07_seatD15_kintsugi_then_demo.md`: follow-up deploy of develop 69f2045 (#1406 + #1404) kintsugi then demo. **Disk does not clear on either box on recorded figures** → at its plan mail, Wednesday CARDS KAM with its measured numbers (options: kintsugi build-cache prune and/or archive oldest rollback sets to G-DRIVE then untag by reference; demo archive `pre-20260910` then untag). Default: nothing freed, nothing built. No GO before his ruling.
- **#1383 HELD** through D 15th's round (Q-1383-15), not just until #1398.
- **Spark screen + brief-writer sub-agent RUNNING** (report → `0_Brain/reference/2026-10-07_spark-screen/SCREEN_1120.md`; brief dirs under `local-model/night/briefs/`). On its return: read every brief whole, then queue via `local-model/spark/queue.md` + start `spark/queue.sh` (README). A rotation KILLS an in-session sub-agent: if this seat must rotate first, the successor re-commissions it.
- OWED (new): the launcher-pulls-before-brief gap (R 7th's deviation) needs a card or a brief-path change; the Secuura launcher is the project's file.
- usage_gate 54% at 11:28. Kam silent since 08:53:04; 0 to reconcile.
- **12:10 UPDATE:** D 15th PLAN CONFIRMED and HOLDING for Kam's card `secuura-followup-deploy-disk-archive-1007` (rec a; default c = nothing freed/built). **At 15:00 AEDT, if still unruled: decide hold vs wrap-cold for D 15th and tell it** (promised in its 01:09Z ANSWER; this session's background timer is the wake, and it dies with a rotation, so a successor owns this line). On (a)/(b): send `GO (Seat D 15th): deploy 69f2045af2a4 to kintsugi` naming the card, his option and the three kintsugi sets (pre-20260910, pre-2026-09-12, pre-20260918), archive to G-DRIVE first; KS-535 C2 control = 7d8958f1e48a608c on both boxes. DEPLOY_SHA stays 69f2045 (ruled (a); #1398's squash is pre-agreed). Demo → D 16th from D 15th's RESUME block.
- **12:10 UPDATE:** 4 Spark passes HELD (READY_KS-1435-…, READY_KS-591-…-CUSTODY-1, READY_KS-1432-… [tier-1 gate, Refs], READY_KS-591-…-TENANT-1 [stacks after tenants-create-status], all `_spark-dsv4flash_`, 2026-10-07). **E 9th raise-brief drafter RUNNING** → `fleet/briefs_staged/2026-10-07_seatE9_raise_spark4.md`; on its return read it whole, rule its open questions in a send amendment, launch with `brief_and_launch.sh --to "Secuura/Blockchain-E"`. If this seat rotated first, re-commission it. Batch its READY with R 7th's PRs 3-5 into one gate where tiers allow (KS-1432 is tier 1).
- R 7th: GO for #1398 sent 00:47:46Z; it is building its deferred tool arms before M-2; next from it: ctx QUESTION before the merge-in, then push, then Wednesday's Actions ADDENDUM releases M-4.

## 🔴 HANDOVER FROM THE MORNING SEAT (rotated ~11:1x 2026-10-07 at ctx ~79%) — FIRST ACTS FOR THE SUCCESSOR
1. **LAUNCH SEAT R 7th** (`Secuura/Blockchain-R`, #1398 then PRs 3-5). Staged, NOT sent: brief `fleet/briefs_staged/2026-10-07_seatR7_merge1398_raise3to5.md` (291 lines) + DRAFT GO `fleet/briefs_staged/2026-10-07_seatR7_GO_1398_DRAFT.md` + drafter report `0_Brain/reference/2026-10-07_seatR7-brief/DRAFTER_REPORT.md`. **READ THE BRIEF WHOLE before launch** (the morning seat did not). Launch with `fleet/brief_and_launch.sh --to "Secuura/Blockchain-R"` (default usage gate; 7d ~52%). The GO is sent only after R 7th's plan confirmation, as a separate mail with subject `GO (Seat R 7th): merge 1398 on gate71`.
   **RULED by the morning seat on the drafter's five questions (write them into the brief's send amendment):**
   (1) the #1398 composed docs are PLACED in `gate71/recomposed_2026-10-07/1398_composed_{flow,cheat}_doc.html`, hash-object = df566caf89168aba… / b938c32912994d03… (== predicted blobs, verified by Wednesday);
   (2) the two extra body edits are KEPT (the landed text must say `28.` after `27.`/KS 1436): body `1398_squash_body.txt` 7,647 B sha256 1a0da3578a906e84d4ea50c8f26799ff17e987e4556f66a9508e61e451132148 (re-hashed by Wednesday);
   (3) the `06-tenant-isolation.sh` tooling pin moved by #1404 is ACCEPTED BY NAME for Q-COVER6 condition (2): #1404 was itself gated (gate71 GO) and merged at Wednesday's GO, and gate71 tested #1398 stacked on #1404;
   (4) `--dev-paths` is re-derived by R 7th from the tool, the drafter's 7 paths are an expectation only;
   (5) track A goes to R 8th unless #1398 lands with R 7th under ~45%.
   T'' for #1398 on develop 69f2045af2a4 = **ce7f6c7bbda2b45491dbd3b184df7a49d4d52528** (kit predict rc 0, drafter; == the earlier SIM). The squash's Actions verdict comes from Wednesday's separate ADDENDUM after R 7th pushes (R 6th's builder reads it only from there; line shape `ACTIONS VERDICT (Wednesday): … 0 new failures.`).
2. **%73 Seat D 14th is WRAPPING** after DEMO DEPLOYED + SWEPT at d75bfe2deb80 (PASS 26 / FAIL 0 / UNMEASURED 1 / X 5; rollback `pre-20261006` fp 513d475d9af77d2d). On its WRAP: re-hash its handover, score, `pane_close.sh %73`. Reported to Kam already.
3. **COMMISSION THE FOLLOW-UP DEPLOY** (October grant, Wednesday's 23:39 ruling (a) told Kam): current develop (≥ 69f2045 = the advisory fix #1406 + #1404) to KINTSUGI first + sweep, then DEMO. Phase 0 re-tag, KS-535, disk measured first; G-DRIVE archive before any deletion (new rule today). Kintsugi's last deploy was d75bfe2deb80 (D 12th).
4. **#1383 (docs PR, head 32e8459bc0f5) is RELEASED by Q8** (demo DEPLOYED). Its merge moves develop: sequence it AFTER #1398 or re-predict #1398 if it lands first.

## MORNING SEAT — STATE (2026-10-07)
- **ACCOUNT:** Kam /login'd ~08:4x (new account, 7d ~52%, renews ~3d 18h); the 100% row EXPIRED (90% stop applies); the 80%-Spark premise ENDED (re-read with Kam). Card `wed-allowance-99pct-three-seats-live-1007` ruled a.
- **develop = 69f2045af2a4** (#1404 squash, verified at source 23:56:29Z) on fa24bddedf3b (#1406 advisory fix, verified 22:10:32Z). The push freeze is LIFTED.
- Scored today: G 3rd 0.94, gate72 1.0, R 6th 0.93 (panes closed). Kam's rulings today: 06:46:01 + 06:46:04 (both cards a), 08:53:04 G-DRIVE rule (filed as a learning).
- **New rule:** archive bulky leftovers to `/Volumes/G-DRIVE` before deleting; clear after ~a month.
- OWED (tooling): the gate-kit template's MERGE ADDENDUM "(#n) lands <= 92" (STANDING_LINES :318 fixed, the template not yet); `cockpit.sh say %<id>` silently no-ops; the announced-step STALL watcher leg (R 6th 09:29 was the 4th instance); F-3 (Secuura docs guard no-ops under a symlinked path) to be filed by R 7th after B (board search first).

## STATE AT THE WRAP (05:3x)
- **develop = b39051390ff6** (#1405, history.md only, on top of 40270d26 = Peter's KS-571 a-d, which REWROTE both platform docs as table matrices with a static guard `systemTest/__tests__/html_docs_matrix.test.sh`, and RENUMBERED the flow doc: tail 22 timings, 23 KS-571, 24 KS-1305). Re-read before anything; Peter merges at night.
- **#1404 (KS-1436, job-06 stderr fix): gate71 GO.** Merge-in **M = 7849f0a23d0609f618736c69a0a33a6a38c6f077** is RETAINED in `worktrees/s-ra4-ks1436`, UNPUSHED. tree(M) = d717255d5376 == T; qm 8/8; the mergein script's record is "first run FAIL 44 of 45 → F-6 (its own added gate) → corrected → standalone PASS" (ruled: keep M, no reset). The **16:20:45Z GO** (`fleet/briefs_staged/2026-10-07_seatR5_GO_1404.md`) STAYS VALID for the next R seat ONLY while develop == b39051390ff6. If develop moved, T is VOID: re-predict with the gate71 kit before any push.
- **#1398 (KS-1136): CONDITIONAL GO**, only after #1404 lands, flow `28.`, re-predicted on the REAL post-#1404 develop with its own qm (ruling W-Q8). Kit prediction 960e71800ea1 is on a SIM base.
- **PRs 3-5 UNRAISED** (KS-998 `29.`, KS-1313 + KS 1326 `25.`, KS-1164 `26.`), RAISE_BASE ruled = live develop (b39051390ff6). All strict-apply. **Q-A owed:** KS-1313's board-account assignment at PR 4 open (third seat to carry it).
- **R 6th** (when the freeze clears): its brief is built from `5_Project_History/HANDOVER-seatR5-2026-10-06.md` (sha256/16 1492bb1a44ed13d4) + R 5th's brief (`fleet/briefs_staged/2026-10-07_seatR5_raise_prs3to5_and_merge_gate71.md`, its WEDNESDAY'S RULINGS section) + the GO. First act: re-read develop; push M only if develop == D AND legs 6/7 are green; then B5 squash; then #1398's GO; then the raises. R 5th's re-keyed tools (ra5 set + the four merge tools with required args) are in its record folder `5_Project_History/2026-10-06_seatR-5th/raise/`.
- **gate71 kit** `fleet/qa-agent/gatesets/2026-10-06_gate71/` (widened; RULINGS has every ruling). Report: `!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-gate71/report.md` (5cbc607a…). Its residue, NOT filed: N-1404-6 (job 06 "tested nothing" reads clean: KS-676 class), N-1398-3 (false cause text), N-1398-5 REPEAT, the aggregate.ts sibling; polish N-1404-3/-4. A board search comes before any filing.
- **#1383** (KS-1401, a docs PR, head 32e8459bc0f5) is held until D 13th DEPLOYED (Q8). If it lands first, #1404's T is void.
- Kintsugi DEPLOYED + SWEPT CLEAN at d75bfe2deb80 (D 12th, 10-06). Rollback `:pre-20261006`.
- Ornith PAUSE_QUEUE to 06:00 10-07 (lapses at the boot). Spark queue EMPTY; the job-06 PASS is consumed (#1404). **The morning seat re-screens for Spark briefs** (Kam 19:30: Spark on all tickets). Any PASS is held; raising waits for the freeze.

## FLOOR AT THE WRAP
%0 wednesday · %1 monitor (D 13th wrapped 05:3x, pane closed). Orphaned DETACHED watchers of wrapped seats F 3rd, E 7th and F 4th were also found and stopped by Wednesday (pids 12127/41307/89913, identity by command line; `inbox_watch` count now 0). No subagents running. R 5th's detached watcher was stopped by Wednesday (pid 22699, identity by command line).

## BUDGET
7d gauge 95% at 05:1x; Kam's 19:30:43 grant lets THIS seat run to 100% until the renewal (~Sun 11 Oct), shaped as card (a): Spark on all tickets, raise/gate/merge/deploy seats only, at most two deployers. **A dependency seat (advisory card (a)) is a BUILD seat, so it needs his tap on that card; the card says so.**

## OWED (Wednesday's own)
- ~~Card for Kam (D 13th's two-history.md finding)~~ DROPPED 2026-10-07 06:06 by the morning seat: the repo copy is PETER's project history (#1405 merged by PeterObeden; last 6 commits author `t`, +0100), the root copy is ours by the layout. Two owners by design, no decision for Kam. Reason in the 10-07 note.
- **Mechanism (four orphaned watchers in one night):** `pane_close.sh` should list the seat's DETACHED `inbox_watch*` processes by its record-folder path and stop them (or refuse until stopped). Today it checks listeners only.
- **Watcher: the "turn ended on an announced next step, nothing running" STALL** (THREE instances in two nights: R 4th, D 12th, R 5th). Promote from candidate to a watcher leg: flag a turn whose last line announces work, with no background job live, as a STALL, not a hold. Claim with Tuesday first (shared tooling).
- Residue cards for Kam (not urgent, after the demo deploy settles): demo's admin seeding protected by ONE variable (NODE_ENV=development, userRepo.ts:1234); GATEWAY_VOUCH_SECRET absent on demo (fail-open).
- `safe_push.sh:108` and `wed_claim.sh:54` still `rebase --autostash` internally.
- A send_brief check flagging "nothing else" near a tool path (ledger w=4); hold_ready.py `--model-tag` for bash_patch.
- Tuesday owes (her pickup) the send_brief.sh `[Wednesday -> …]` prefix fix; she claims it with Wednesday first.

## OWED (board-pass list, unfiled)
- namecheck's +8 subject gate refuses 85-92 char subjects.
- history.md's stale D 10th and R 3rd handover shas (the files were edited after the history entries).
- BACKLOG.md lacks the CI findings.
- The 6 shell suites red on CI, green in-hook.
- 11 overlapping lockfile PRs.
- `dev-reload.sh:73` UTF-8 unbound variable.
- KS-729 past due.
- Signatory routes' org-membership check.
- `--no-optional-locks` stale-stat blindness.
- Leg-6 CLEANUP advisory: 15 stale baseline rows (12 KS-470, 3 KS-559).
- `git for-each-ref` `*` does not cross `/`: STANDING_LINES candidate.
- gate71 residue: Q1 (persisting unreadable artefact exits 0 on run 2), Q3 (`ci/aggregate.ts:241-243` skipping unparseable).
- `tmux display-message` without `-t` returns the active pane: six recurrences across seats, a tool default that is wrong.
- KS-1422 stale origin/develop. Ledger w=4: a mechanism for "ruling on a seat's tool unread".

## STANDING NOTES
- Pathspec-only commits; pull with `tools/safe_pull.sh`. decisions.json and the chat stores are STATE.
- A seat CANNOT read its own context: gates are mail handshakes, and Wednesday reads the pane.
- Receipts quoting a send's output are written AFTER the output is visible. Close a gate's pane on reading its verdict. Quoted heredocs only (inject live values by sed afterwards).
- Before any GO, open the brief's GO section and copy its required shape.
- A develop move is identified in Wednesday's OWN scratch clone, never by a write verb in the project checkout.
- After a pane close, check the seat's watcher: a detached one (tty ??) survives and stays keyed to the pane NAME.
